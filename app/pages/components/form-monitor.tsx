import { useState } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Pie } from "react-chartjs-2";
import { Button, Form, Spinner } from "react-bootstrap";
import NewWindow from 'react-new-window'
ChartJS.register(ArcElement, Tooltip, Legend);
export default function FormMonitor(styles: any) {
  const [url, setUrl] = useState("");
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [isChatOpen, setChatOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [ isUrlValid, setIsUrlValid ] = useState(true)
  const urlPatternValidation = ( URL: string) => {
    const regex = new RegExp('^(https\\:\\/\\/www\\.youtube\\.com\\/watch\\?v=)([a-zA-Z0-9_\\-]+)$', 'gm');    
    return regex.test(URL);
  };
  const setAndValidateUrl = (event : any) => {
    setUrl(event.target.value)
    setIsUrlValid((url != ""|| url != undefined) && urlPatternValidation(event.target.value))
  }
  const defaultState = () => {
    return {
      rawData: {
        bad: 0,
        neutral: 0,
        good: 0,
      },
      chartData: {
        labels: ["Bad", "Neutral", "Good"],
        datasets: [
          {
            label: "% Interactions",
            data: [0, 0, 0],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
            ],
          },
        ],
      },
    };
  };
  const [chatAnalized, setChatAnalized] = useState(defaultState());
  const startMonitor = (e: any) => {
    e.preventDefault()    
    if(!(urlPatternValidation(url) && (url != "" || url != undefined)) ) return;
    setIsLoading(true);
    fetch(`http://localhost:8000/start/monitor?url=${url}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Aquí puedes usar los datos que recibiste de la API
        console.log(data);
        setIsMonitoring(true);
        setIsLoading(false);
      })
      .catch((error) => {
        // Manejo de errores
        console.error(error);
        setIsLoading(false);
      });
  };
  const stopMonitor = (e: any) => {
    e.preventDefault();
    fetch("http://localhost:8000/stop/monitor", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Aquí puedes usar los datos que recibiste de la API
        console.log(data);
        setIsMonitoring(false);
        setUrl("");
        setIsLoading(false);
        setChatAnalized(defaultState());
      })
      .catch((error) => {
        // Manejo de errores
        console.error(error);
        setIsMonitoring(false);
        setIsLoading(false);
        setChatAnalized(defaultState());
      });
  };
  const analizeChat = (e: any) => {
    e.preventDefault();
    setIsLoading(true);
    fetch("http://localhost:8000/chat/analize")
      .then((response) => response.json())
      .then((data) => {
        // Aquí puedes usar los datos que recibiste de la API
        console.log(data);
        const bad = +(data.results.NEG * 100).toFixed(2);
        const neutral = +(data.results.NEU * 100).toFixed(2);
        const good = +(data.results.POS * 100).toFixed(2);
        setChatAnalized({
          rawData: {
            bad: bad,
            neutral: neutral,
            good: good,
          },
          chartData: {
            labels: ["Bad", "Neutral", "Good"],
            datasets: [
              {
                label: "% Interactions",
                data: [bad, neutral, good],
                backgroundColor: [
                  "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 206, 86, 0.2)",
                ],
              },
            ],
          },
        });
        setIsLoading(false);
      })
      .catch((error) => {
        // Manejo de errores
        console.error(error);
        setIsLoading(false);
      });
  };
  return (
    <Container>
      <Row>
        <Col sm="4">
          <Form>
            <Form.Group>
              <Form.Control
                type="text"
                value={url}
                onChange={setAndValidateUrl}
                readOnly={isMonitoring}
                placeholder="YouTube Live URL"
              ></Form.Control>
              {!isUrlValid ?(
              <div style={{ color: "#F61C04" }}>URL is not valid.</div>
              ) :null}
              </Form.Group>
              <Form.Group>
              <Button
                variant="primary"
                onClick={startMonitor}
                disabled={isMonitoring}
              >
                Monitor
              </Button> { ' ' }
              <Button
                variant="danger"
                onClick={stopMonitor}
                disabled={!isMonitoring}
              >
                {isMonitoring ? (
                  <Spinner
                    animation="grow"
                    as="span"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                ) : null}
                Stop
              </Button>{ ' ' }
              <Button
                variant="success"
                onClick={analizeChat}
                disabled={!isMonitoring}
              >
                Analize chat
              </Button> { ' ' }
              <Button onClick={ () => setChatOpen(true) } disabled={!(urlPatternValidation(url) && (url != "" || url != undefined))}>Open chats </Button>
              { isChatOpen ?
              <NewWindow url={`https://www.youtube.com/live_chat?is_popout=1&v=${url.split("=")[1]}`}  onOpen={() => setChatOpen(false)}>
                <h1>Hi 👋</h1>
              </NewWindow> : null
              }
            </Form.Group>
          </Form>
        </Col>
        <Col sm="4">
          <iframe
            id="videoLive"
            width="560"
            height="315"
            src={`https://www.youtube.com/embed/${url.split("=")[1]}?autoplay=1`}
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          ></iframe>
        </Col>
      </Row>
      <Row>
        <Col sm="1">{isLoading ? <Spinner animation="border" /> : null}</Col>
        <Col sm="3">
          <Row>
            <Col sm="4">Bad</Col>
            <Col sm="4">Neutral</Col>
            <Col sm="4">Good</Col>
          </Row>
          <Row>
            <Col sm="4">{chatAnalized.rawData.bad}%</Col>
            <Col sm="4">{chatAnalized.rawData.neutral}%</Col>
            <Col sm="4">{chatAnalized.rawData.good}%</Col>
          </Row>
        </Col>
        <Col sm="4">
          <Pie data={chatAnalized.chartData} />
        </Col>
      </Row>
    </Container>
  );
}
