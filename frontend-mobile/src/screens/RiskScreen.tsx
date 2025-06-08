import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet, FlatList } from 'react-native';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../app/App';

const API_BASE = process.env.EXPO_PUBLIC_API_BASE || 'http://localhost:8000';

export default function RiskScreen() {
  const navigation = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
  const [risk, setRisk] = useState<number | null>(null);
  const [drivers, setDrivers] = useState<{ feature: string; impact: number }[]>([]);
  const [leadTime, setLeadTime] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  async function fetchRisk() {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/v1/risk/latest`, {
        headers: { Authorization: `Bearer dev-token` },
      });
      setRisk(res.data.risk_percentage);
      setDrivers(res.data.top_drivers);
      setLeadTime(res.data.lead_time_hours);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchRisk();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Current Risk</Text>
      {risk !== null ? (
        <Text style={styles.risk}>{Math.round(risk * 100)}%</Text>
      ) : (
        <Text>Loading...</Text>
      )}
      {leadTime !== null && (
        <Text style={styles.lead}>Estimated lead time: {leadTime.toFixed(1)} h</Text>
      )}
      <Text style={styles.subtitle}>Top Drivers</Text>
      <FlatList
        data={drivers}
        keyExtractor={(item) => item.feature}
        renderItem={({ item }) => (
          <View style={styles.driverRow}>
            <Text style={styles.feature}>{item.feature}</Text>
            <Text style={styles.impact}>{(item.impact * 100).toFixed(1)}%</Text>
          </View>
        )}
      />
      <Button title="Refresh" onPress={fetchRisk} disabled={loading} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 20,
    marginBottom: 8,
    fontWeight: '600',
  },
  risk: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#c92a2a',
  },
  lead: {
    marginTop: 8,
    marginBottom: 16,
    fontSize: 16,
  },
  subtitle: {
    marginTop: 16,
    fontSize: 18,
    fontWeight: '600',
  },
  driverRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 4,
  },
  feature: {
    fontSize: 16,
  },
  impact: {
    fontSize: 16,
    fontWeight: 'bold',
  },
});