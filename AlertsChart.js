import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AlertsChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#233554" />
        <XAxis dataKey="time" stroke="#a8b2d1" />
        <YAxis allowDecimals={false} stroke="#a8b2d1" />
        <Tooltip contentStyle={{ backgroundColor: '#112240', borderColor: '#233554' }} />
        <Legend />
        <Line 
          type="monotone" 
          dataKey="alerts"
          stroke="#64ffda"
          strokeWidth={2}
          activeDot={{ r: 8 }} 
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default AlertsChart;