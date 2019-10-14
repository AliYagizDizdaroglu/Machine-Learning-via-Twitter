import politics from './dataset/politics';
import database from './firebase/firebase';
import getWordCount from './utils/getWordCount';
import readPoliticsData from './api/politics.api';

// const politicsWordCounts = getWordCount(politics);

// database
//   .collection('bitirme')
//   .doc('politics')
//   .set({
//     politicsWordCounts,
//   })
//   .then(() => {
//     console.log('Document successfully written!');
//   })
//   .catch(error => {
//     console.error('Error writing document: ', error);
//   });

const input = 'ak parti bir partidir';

readPoliticsData().then(result => {
  result.forEach(a => {
    const datas = a.data();

    const parseInput = input.split(' ');

    parseInput.forEach(parseWord => {
      const rate =
        datas.politicsWordCounts[parseWord] / Object.keys(datas.politicsWordCounts).length;

      console.log(parseWord + ' ' + rate / 4);
    });
  });
});
