import { StatusBar } from 'expo-status-bar';
import React, { useRef, useState } from 'react';
import { StyleSheet, Text, View, Dimensions, Animated, Button, Image } from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import { NavigationContainer } from '@react-navigation/native';
import { InAppNotificationProvider } from 'react-native-in-app-notification';
import { API_URL } from '../constants'

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

const nextMove = async (moveHistory, playerId) => {
  const response = await fetch(API_URL + '/generateNextMove/'
    + JSON.stringify({ board: moveHistory, player: playerId }), {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    // body data type must match "Content-Type" header
  });
  return response.json();
}

const rateOpp = async (moveHistory) => {
  const response = await fetch(API_URL + '/' + moveHistory, {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    //body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json();
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
function Game({ route, navigation }) {
  const { playerId } = route.params;

  const w = 7, h = 6;
  const [grid, setGrid] = useState(createGrid(w, h));
  const [nextColor, setNextColor] = useState('red');
  const [moves, setMoves] = useState('')
  const [gameOver, setGameOver] = useState(false);
  const [gameOverMessage, setGameOverMessage] = useState(null);
  const [didWin, setDidWin] = useState(false);

  const onPress = async (row, col) => {
    if (gameOver) return;
    //console.log(row, col)
    const gridCopy = copyGrid(grid);
    if (addDisk(gridCopy, col, nextColor)) {
      const qmoves = moves + (col + 1)



      const move = await nextMove(qmoves, playerId)
      addDisk(gridCopy, move - 1, 'yellow');
      setGrid(gridCopy);
      console.log(move)
      setMoves(qmoves + move)

      if (checkGame(gridCopy, 'red')) {
        setGameOver(true)
        setDidWin(true)
        setGameOverMessage('You win! Good work.')
        //navigation.navigate('YouWin', {playerId});
      } else if (checkGame(gridCopy, 'yellow')) {
        setGameOver(true)
        setDidWin(false)
        setGameOverMessage('You lose! Good work.')
        //navigation.navigate('GameOver', {playerId});
      }
      // setNextColor(nextColor === 'red' ? 'yellow' : 'red');

      //console.log(gridCopy)
    } else {
      // console.log('hasnthappened')
    }
  }

  const clearGame = () => {
    setGrid(createGrid(w, h))
    setMoves('');
    setGameOver(false);
  }
  return (
    <>
      <View style={styles.goc}>
        {gameOver ?
          <>
            <Text style={styles.got}>{gameOverMessage}</Text>
            <Text>Thanks for playing against the bot. We now have a rough idea of how you play.
            Your skill has now been analyzed, quantified and stored. Thanks from the linearly regressive team :)
            </Text>
            <Button
              onPress={clearGame}
              title="Play Again"
              color="#841584"
              accessibilityLabel="Learn more about this purple button"
            />
          </> : undefined}
      </View>
      <View style={styles.container}>
        {grid.map((row, rowi) => <View style={styles.row} key={rowi}>
          {row.map((circle, coli) => {
            const style = {
              'empty': styles.circlee,
              'red': styles.circler,
              'yellow': styles.circley
            }[circle];

            return <View style={styles.bg}><View onTouchStart={() => onPress(rowi, coli)} style={style} key={coli}></View></View>
          })}
        </View>)}
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 0,
    flexDirection: 'column',
    backgroundColor: 'blue',
    justifyContent: 'flex-end',
    padding: 30,
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
    backgroundColor: 'white',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'center',
  },

  bg: {
    backgroundColor: 'blue',
    padding: 3
  },
  got: {
    alignItems: 'center',
  },
  goc: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    flex: 1
  }
});

export default Game;