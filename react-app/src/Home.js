import React, {Component} from 'react';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class CreateHome extends Component {
    render() {
    return (
        <div>
            <header>
                <h1>OpenCitations in Charts</h1>
                <nav>
                    <li>Home</li>
                    <li>About</li>
                </nav>
            </header>
                <h2>Explore the COCI dataset of OpenCitations</h2>
                <Container fluid="md">
                    <Row>
                        <Col>Blah blah blah something about COCI and OpenCitations</Col>
                    </Row>
                    </Container>
                <span><Button variant="primary">Primary</Button>{''}</span>
        </div>
    )};
}

export default CreateHome;