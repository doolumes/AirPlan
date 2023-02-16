/* istanbul ignore file */
import express from 'express';
import cors from 'cors';
import { env } from './env';
import { logger } from './logger';
import { flights } from './api/flights';
import { airportRouter } from './api/airports';
import axios from 'axios';

const port = env.port || '4000';

const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (_: express.Request, res: express.Response) => {
  axios.get('http://localhost:4000/flights', {
    params: {
      date: "2020-01-01"
    }
  })
  .then(function (response) {
    res.send(response.data);
    console.log(response);
  })
  .catch(function (error) {
    res.send(`err: ${error}`)
    console.log(error);
  })
  .then(function () {
    // always executed
  });
  // res.send('👋 Hello WOrld');
});

app.use('/flights', flights);

app.use('/airports', airportRouter);

app.listen(port, () => {
  logger.notice(`🚀 Listening at http://localhost:${port}`);
});
