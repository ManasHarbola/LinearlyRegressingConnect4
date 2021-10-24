import { StatusBar } from 'expo-status-bar';
import React, { useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Animated, Button } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';
import { InAppNotificationProvider } from 'react-native-in-app-notification';

function YouWin({ route, navigation }) {
  return (
    <View>
      <Text style = {styles.winMessage}>You Won! Want to play more for us to better simulate you?</Text>
      <Button style = {styles.winMessage}
        title="Play Again"
        color="blue"
        onPress={() => {
          navigation.navigate('Arena');
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: '#fff',
    justifyContent: 'flex-end',
    padding: 25,
  },
  play: {
    color: 'blue'
  }
  ,
  winMessage: {
    color: 'white',
    backgroundColor: 'blue',
    justifyContent: 'center'
  }
});

export default YouWin;