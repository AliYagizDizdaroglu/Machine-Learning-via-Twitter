// import politics from './dataset/politics';
// import economy from './dataset/economy';
// import science from './dataset/science';
// import sport from './dataset/sport';
// import music from './dataset/music';
// import database from './firebase/firebase';
// import getWordCount from './utils/getWordCount';
import firebase from 'firebase';
import config from './firebase/config';

firebase.initializeApp(config);

const database = firebase.firestore();

// const data = getWordCount(music);

// database
//   .collection('bitirme')
//   .doc('music')
//   .set({
//     data,
//   })
//   .then(() => {
//     console.log('Document successfully written!');
//   })
//   .catch(error => {
//     console.error('Error writing document: ', error);
//   });

Object.size = obj => {
  let size = 0;
  let key;
  // eslint-disable-next-line no-restricted-syntax
  for (key in obj) {
    // eslint-disable-next-line no-prototype-builtins
    if (obj.hasOwnProperty(key)) size += 1;
  }
  return size;
};

const input =
  'Usülsüz ihale oyunu Haydarpaşa İstanbul halkına işadamlarına sermaye peşkeş çekmek isteyenler';

const DATASETNAME = ['politics', 'music', 'economy', 'sport', 'science'];
const databaseData = [];

DATASETNAME.forEach(datasetName => {
  database
    .collection('bitirme')
    .doc(datasetName)
    .get()
    .then(datas => {
      if (!datas.exists) return;

      const realData = datas.data().data;

      const testData = input.split(' ');
      let rate = 0;

      testData.forEach(word => {
        console.log(`${datasetName} ${realData[word]}`);
        rate +=
          parseFloat(realData[word] === undefined ? 0 : realData[word]) /
          parseFloat(Object.size(realData));
      });

      const element = {};

      element.dataset = datasetName;
      element.value = rate / testData.length;

      databaseData.push(element);
    });
});

console.log(databaseData);
