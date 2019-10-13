import readPoliticsData from './api/politics.api';

import './app.scss';

const data = readPoliticsData();

data.then(result => {
  result.forEach(e => {
    console.log(e.data());
  });
});
