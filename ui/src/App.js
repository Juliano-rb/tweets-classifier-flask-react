import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';
import { Tweet } from 'react-twitter-widgets'

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        tweet: ''
      },
      result: ""
    };
  }
  getTweetId = (link)=>{
    const parts = link.split('/')
    const partsCount = parts.length
    const id = parts[partsCount-1]

    return id
  }
  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    const tweetId = this.getTweetId(value)
    //parsing string to get tweet id
    console.log(formData)
    formData[name] = tweetId;
    ReactDOM.render(<Tweet name='tweetWidget' tweetId={tweetId}/>, document.getElementById('tweet'))
    this.setState({
      formData
    });
  }
  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });

    const url = process.env.REACT_APP_API_URL || "http://localhost:5000";
    fetch(url+'/prediction/', 
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return (
      <Container>
        <div>
          <h1 className="title">Tweet Sentiment Analysis</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Tweet link:</Form.Label>
                <Form.Control 
                  type="text" 
                  placeholder="Insert a tweet link" 
                  name="tweet"
                  value={formData.tweet}
                  onChange={this.handleChange} />
              </Form.Group>
            </Form.Row>
            <Form.Row>
              <Container id='tweet' className="tweetShow">
              </Container>
            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Making prediction' : 'Predict' }
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Reset prediction
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
        </div>
      </Container>
    );
  }
}

export default App;
