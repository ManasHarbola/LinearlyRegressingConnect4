import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, Dimensions, Button, Image } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as Location from 'expo-location';
import { getDistance } from 'geolib';
import Game from './components/Game'
import { Notifications } from 'expo';
import * as Permissions from 'expo-permissions';
import { InAppNotificationProvider } from 'react-native-in-app-notification';
import AsyncStorage from '@react-native-async-storage/async-storage';
import YouWin from './components/YouWin'
import GameOver from './components/GameOver'
import { Alert } from 'react-native';


export const API_URL = 'http://8efb-2610-148-1f02-7000-3da7-9f21-15ea-f7d8.ngrok.io'

const Stack = createNativeStackNavigator();

async function registerForPushNotificationsAsync() {
  const { status } = await Permissions.getAsync(Permissions.NOTIFICATIONS);
  let finalStatus = status;

  if (status !== 'granted') {
    const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);
    finalStatus = status;
  } funwithncr, hireme
}
export default function App() {


  useEffect(() => {
    const promptUser = () => {
      Alert.prompt(
        "Name",
        "Enter Your name to play:",
        [
          {
            text: "Set Name",
            onPress: async value => {
              try {
                await AsyncStorage.setItem('@name', value)
              } catch (e) {
                // saving error
              }
            }
          }
        ],
        "plain-text"
      );
    }
    (async () => {
      try {
        const value = await AsyncStorage.getItem('@name')
        if (value !== null) {
          // value previously stored
        } else {
          promptUser();
        }
      } catch (e) {
        // error reading value
      }
    })()
  })

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="World" component={World} />
        <Stack.Screen name="Arena" component={Arena} />
        <Stack.Screen name="Game" component={Game} />
        <Stack.Screen name="YouWin" component={YouWin} />
        <Stack.Screen name="GameOver" component={GameOver} />

      </Stack.Navigator>
    </NavigationContainer>
  );
}

function World({ navigation }) {
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const [isActive, setActive] = useState(true);

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setTimeout(() => {
        (async () => {
          let { status } = await Location.requestForegroundPermissionsAsync();
          if (status !== 'granted') {
            setErrorMsg('Permission to access location was denied');
            return;
          }
          let location = await Location.getCurrentPositionAsync({});
          setLocation(location);
        })();
      }, 10000);
    } else if (!isActive) {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, location, errorMsg]);

  useEffect(() => {
    console.log("Hello")
  }, [location])

  const arenas = [{
    coordinate: {
      latitude: 33.774691,
      longitude: -84.397323,
    },
    title: "Tech Green Battlefield",
    description: "asdf",
  },
  {
    coordinate: {
      latitude: 33.7772198,
      longitude: -84.3963587,
    },
    title: "Klaus Arena",
    description: "asdf",
  },]

  const isArenaValid = (arena) => {
    if (!location || !location.coords || !arena || !arena.coordinate) {
      console.log("oof")
      return
    }
    const distInMeters = getDistance(
      { ...location.coords },
      { ...arena.coordinate }
    );
    if (distInMeters < 150) {
      return true;
    }
    return false;
  }

  const onPress = (arena) => {
    if (isArenaValid(arena)) {
      navigation.navigate('Arena');
    }
  }

  return (<MapView style={styles.map} showsUserLocation >
    {
      arenas.map(arena => <Marker
        key={arena.title}
        coordinate={arena.coordinate}
        title={arena.title}
        description={arena.description}
        onCalloutPress={() => onPress(arena)}
      >
        <Image
          source={require('./assets/connect-4-icon.png')}
          style={{ height: 30, width: 30, opacity: isArenaValid(arena) ? 1 : .3 }}
        />
      </Marker>)
    }
  </MapView >)
}

function Arena({ navigation }) {

  useEffect(() => {
    Alert.prompt(
      "Train your Agent",
      "To play at this arena, first play against an AI.",
      [
        {
          text: "Play",
          onPress: async value => {
            navigation.navigate('Game', {playerId: 'id'});
          }
        }
      ],
      "plain-text"
    );
  }, [])
  
  return (
    <View style={styles.centerItems}>
      <Text style={styles.welcomeMessage}>Welcome to Tech Green Arena</Text>
      <Text style={styles.topPlayer} >Top Players</Text>
      <Text style={styles.leaderboard}>First: </Text>
      <Text style={styles.leaderboard}>Second: </Text>
      <Text style={styles.leaderboard}>Third: </Text>

      <Button style={styles.startGame}
        title="Play Game"
        color="#f194ff"
        onPress={() => {
          navigation.navigate('Game');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
  welcomeMessage: {
    color: 'lightgreen',
    fontWeight: 'bold',
    fontSize: 40,
    alignItems: 'center',
  },
  topPlayer: {
    color: 'black',
    fontSize: 30,
    alignItems: 'center'
  },
  leaderboard: {
    color: 'blue',
    fontSize: 20
  }
  ,
  startGame: {
    color: 'white',
    backgroundColor: 'black'
  }
  ,
  centerItems: {
    alignItems: 'center'
  }
});