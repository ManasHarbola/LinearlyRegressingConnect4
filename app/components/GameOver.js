import { StatusBar } from 'expo-status-bar';
import React, { useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Animated, Button } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';

function GameOver({ route, navigation }) {
  const { playerId } = route.params;
  if (playerId === 'id') {
    return (
      <View>
        <Text style = {styles.winMessage}>Thanks for playing against the bot. Your skill now analyzed, quantified and stored. 
        We now know have a rough idea of how you play, and will keep it in our records. Thanks from the linearly regressive team :)
        </Text>
        <Text>Go back to the arena to play </Text>
        <Button style = {styles.startGame}
          title="View Arena"
          color="#f194ff"
          onPress={() => {
            navigation.navigate('Arena');
          }}
        />
      </View>
    );
  }

  return (
    <View>
      <Text style = {styles.winMessage}>You Lose!</Text>
      <Button style = {styles.startGame}
        title="Play Again"
        color="#f194ff"
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
  winMessage: {
    color: 'yellow',
    backgroundColor: 'black',
    fontSize: 30
  }
});

export default GameOver;