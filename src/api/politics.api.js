import database from '../firebase/firebase';

const readPoliticsData = async () => {
  const response = await database.ref('politics').once('value');

  const result = response.val();

  return result;
};

export default readPoliticsData;
