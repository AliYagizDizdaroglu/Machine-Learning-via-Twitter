import database from '../firebase/firebase';

const readPoliticsData = async () => {
  try {
    const data = await database.collection('bitirme').get();

    return data;
  } catch (err) {
    // TODO: Error Handle
    // eslint-disable-next-line
    console.log(err);
  }
};

export default readPoliticsData;
