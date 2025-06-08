import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function NudgeScreen() {
  // In a real app, nudge data would come from push notifications or API polling.
  // For demonstration we show static text.
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Nudge</Text>
      <Text style={styles.body}>Stay hydrated and stretch for 5 minutes to reduce your flare‑up risk.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 12,
  },
  body: {
    fontSize: 18,
    textAlign: 'center',
  },
});