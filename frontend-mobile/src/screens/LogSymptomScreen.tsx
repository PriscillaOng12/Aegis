import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { Slider } from '@react-native-community/slider';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../app/App';

const API_BASE = process.env.EXPO_PUBLIC_API_BASE || 'http://localhost:8000';

export default function LogSymptomScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const [pain, setPain] = useState(0);
  const [fatigue, setFatigue] = useState(0);
  const [nausea, setNausea] = useState(0);
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function submit() {
    setSubmitting(true);
    try {
      await axios.post(`${API_BASE}/v1/symptoms`, {
        pain,
        fatigue,
        nausea,
        notes,
        timestamp: new Date().toISOString(),
      }, {
        headers: { Authorization: `Bearer dev-token` },
      });
      setPain(0);
      setFatigue(0);
      setNausea(0);
      setNotes('');
      navigation.navigate('Risk');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Pain: {pain}</Text>
      <Slider
        minimumValue={0}
        maximumValue={10}
        step={1}
        value={pain}
        onValueChange={setPain}
      />
      <Text style={styles.label}>Fatigue: {fatigue}</Text>
      <Slider
        minimumValue={0}
        maximumValue={10}
        step={1}
        value={fatigue}
        onValueChange={setFatigue}
      />
      <Text style={styles.label}>Nausea: {nausea}</Text>
      <Slider
        minimumValue={0}
        maximumValue={10}
        step={1}
        value={nausea}
        onValueChange={setNausea}
      />
      <Text style={styles.label}>Notes</Text>
      <TextInput
        style={styles.textInput}
        multiline
        numberOfLines={4}
        placeholder="Describe your symptoms"
        value={notes}
        onChangeText={setNotes}
      />
      <Button title={submitting ? 'Submitting...' : 'Submit'} onPress={submit} disabled={submitting} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  label: {
    fontSize: 16,
    marginTop: 16,
  },
  textInput: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 4,
    padding: 8,
    marginTop: 8,
    marginBottom: 16,
  },
});