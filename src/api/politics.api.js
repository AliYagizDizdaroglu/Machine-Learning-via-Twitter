import database from '../firebase/firebase';

const readPoliticsData = async () => {
  await database
    .collection('bitirme')
    .get()
    .then(querySnapshot => {
      querySnapshot.forEach(doc => {
        console.log(doc.data());
      });
    });
};

export default readPoliticsData;
