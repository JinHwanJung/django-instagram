import React, { Component } from 'react';
import {
    StyleSheet, Text, View, StatusBar,
} from 'react-native';
import Button from '../button';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#CE0B24',
    },
    section: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    upper: {
        flex: 2,
    },
    time: {
        color: 'white',
        fontSize: 120,
        fontWeight: '100',
    },
});

class Timer extends Component {
    render() {
        return (
            <View style={styles.container}>
                <StatusBar barStyle="light-content" />
                <View style={[styles.section, styles.upper]}>
                    <Text style={styles.time}>25:00</Text>
                </View>
                <View style={styles.section}>
                    <Button iconName="play-circle" onPress={() => alert("It works!")}/>
                    <Button iconName="stop-circle" onPress={() => alert("It works!")}/>
                </View>
            </View>
        );
    }
}

export default Timer;
