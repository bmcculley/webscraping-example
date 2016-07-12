/**
 * This file provided by Facebook is for non-commercial testing and evaluation
 * purposes only. Facebook reserves all rights not expressly granted.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

var Post = React.createClass({
  
  render: function() {
    return (
      <div className="post">
        <h2 className="postTitle">
          {this.props.title}
        </h2>
        <div className="postContent" dangerouslySetInnerHTML={{__html: this.props.children}} />
      </div>
    );
  }
});

var PostContainer = React.createClass({
  loadPostsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data.posts});
        this.setState({nextPage: data.nextPage});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadPostsFromServer();
    setInterval(this.loadPostsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="container">
        <div className="postBox">
          <h1 className="site-title">Webscraping Tutorial</h1>
          <PostList data={this.state.data} />
        </div>
        <div className="pagination">
          <NextPage data={this.state.nextPage} />
        </div>
      </div>
    );
  }
});

var PostList = React.createClass({
  render: function() {
    var postNodes = this.props.data.map(function(post) {
      return (
        <Post title={post.title} key={post.id}>
          {post.content}
        </Post>
      );
    });
    return (
      <div className="postList">
        {postNodes}
      </div>
    );
  }
});

var NextPage = React.createClass({
  handleClick: function() {
    ReactDOM.render(
      <PostContainer url={"/api?page=" + this.props.data} />,
      document.getElementById('content')
    );
  },
  render: function() {
    return (
        <a className="next" onClick={this.handleClick} >Next</a>
    );    
  },
});


ReactDOM.render(
  <PostContainer url="/api" pollInterval={2000} />,
  document.getElementById('content')
);