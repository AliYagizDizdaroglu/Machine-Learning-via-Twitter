import firebase from 'firebase';
import config from './config';

firebase.initializeApp(config);

const database = firebase.firestore();

export default database;
