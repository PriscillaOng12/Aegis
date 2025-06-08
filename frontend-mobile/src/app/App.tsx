import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LogSymptomScreen from '../screens/LogSymptomScreen';
import RiskScreen from '../screens/RiskScreen';
import NudgeScreen from '../screens/NudgeScreen';

export type RootStackParamList = {
  LogSymptom: undefined;
  Risk: undefined;
  Nudge: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="LogSymptom">
        <Stack.Screen name="LogSymptom" component={LogSymptomScreen} options={{ title: 'Log Symptom' }} />
        <Stack.Screen name="Risk" component={RiskScreen} options={{ title: 'Risk Score' }} />
        <Stack.Screen name="Nudge" component={NudgeScreen} options={{ title: 'Nudge' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}