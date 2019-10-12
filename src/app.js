import readPoliticsData from './api/politics.api';

try {
  const data = readPoliticsData();

  console.log(data);
} catch (error) {
  console.log(error);
}
