import { StatusBar } from 'expo-status-bar';
import React, { useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Animated, Button } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';

function GameOver({ navigation }) {
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
});

export default GameOver;