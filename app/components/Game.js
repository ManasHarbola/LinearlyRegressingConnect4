import { StatusBar } from 'expo-status-bar';
import React, { useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Animated, Button } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';
import { InAppNotificationProvider } from 'react-native-in-app-notification';

// disks are strings: 'red', 'yellow', 'empty'

function addDisk(grid, col, toplace) {
  let spot = -1;
  for (let i = 0; i < grid.length; i++) {
    if (grid[i][col] === 'empty') {
      spot = i;
    }
  }
  if (spot !== -1) {
    grid[spot][col] = toplace;
    return true;
  }
  return false;
}

function createGrid(w, h) {
  const ret = [];
  for (let r = 0; r < h; r++) {
    const row = [];
    for (let c = 0; c < w; c++) {
      row.push('empty');
    }
    ret.push(row);
  }
  return ret;
}

function copyGrid(grid) {
  return grid.map(row => [...row]);
}
function checkGame(board, color) {
  //Horizontal Check
  for (var i = 0; i < 6; i++) { // getWidth() - 3
    for (var j = 0; j < 4; j++) {
      if (board[i][j] === color && board[i][j + 1] === color && board[i][j + 2] === color && board[i][j + 3] === color) {
        return true;
      }
    }
  }
  //vertical Check
  for (var i = 0; i < 3; i++) {
    for (var j = 0; j < 7; j++) {
      if (board[i][j] === color && board[i + 1][j] === color && board[i + 2][j] === color && board[i + 3][j] === color) {
        return true;
      }
    }
  }
  //ascendingDiagonalCheck
  for (var i = 3; i < 6; i++) {
    for (var j = 0; j < 4; j++) {
      if (board[i][j] === color && board[i - 1][j + 1] === color && board[i - 2][j + 2] === color && board[i - 3][j + 3] === color)
        return true;
    }
  }
  //descendingDiagonalCheck
  for (var i = 3; i < 6; i++) {
    for (var j = 3; j < 7; j++) {
      if (board[i][j] === color && board[i - 1][j - 1] === color && board[i - 2][j - 2] === color && board[i - 3][j - 3] === color)
        return true;
    }
  }
  return false;
}
function Game({ navigation }) {
  const w = 7, h = 6;
  const [grid, setGrid] = useState(createGrid(w, h));
  const [nextColor, setNextColor] = useState('red');

  const onPress = (row, col) => {
    //console.log(row, col)
    const gridCopy = copyGrid(grid);
    if (addDisk(gridCopy, col, nextColor)) {
      setGrid(gridCopy);
      if (checkGame(gridCopy, 'red')) {
        navigation.navigate('YouWin');
      } else if (checkGame(gridCopy, 'yellow')) {
        navigation.navigate('GameOver');
      }
      setNextColor(nextColor === 'red' ? 'yellow' : 'red');

      //console.log(gridCopy)
    } else {
      // console.log('hasnthappened')
    }
  }

  return (
    <>
      <Button
        onPress={() => setGrid(createGrid(w,h))}
        title="clear"
        color="#841584"
        accessibilityLabel="Learn more about this purple button"
      />

      <View style={styles.container}>
        {grid.map((row, rowi) => <View style={styles.row} key={rowi}>
          {row.map((circle, coli) => {
            const style = {
              'empty': styles.circlee,
              'red': styles.circler,
              'yellow': styles.circley
            }[circle];

            return <View onTouchStart={() => onPress(rowi, coli)} style={style} key={coli}></View>
          })}
        </View>)}
      </View>
    </>
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
  circler: {
    width: 45,
    height: 45,
    borderRadius: 45 / 2,
    backgroundColor: "red",
  },
  circley: {
    width: 45,
    height: 45,
    borderRadius: 45 / 2,
    backgroundColor: "yellow",
  },
  circleg: {
    width: 45,
    height: 45,
    borderRadius: 45 / 2,
    opacity: .2,
    backgroundColor: "black",
  },
  circlee: {
    width: 45,
    height: 45,
    borderRadius: 45 / 2,
    backgroundColor: "rgba(0,0,0,0)",
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
});

export default Game;