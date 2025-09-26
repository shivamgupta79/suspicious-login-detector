import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// This component takes an array of 'data' to display on the chart
const LineChartComponent = ({ data }) => {
  return (
    // ResponsiveContainer ensures the chart adjusts to the size of its parent container
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        {/* The background grid */}
        <CartesianGrid strokeDasharray="3 3" />
        
        {/* The horizontal X-axis, using the 'name' key from our data */}
        <XAxis dataKey="name" />
        
        {/* The vertical Y-axis */}
        <YAxis />
        
        {/* The tooltip that appears when you hover over a data point */}
        <Tooltip />
        
        {/* The legend that labels the lines */}
        <Legend />
        
        {/* The actual line on the chart */}
        <Line 
          type="monotone" 
          dataKey="value" // This should match the key in our data for the y-axis value
          stroke="#8884d8" // Color of the line
          activeDot={{ r: 8 }} 
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default LineChartComponent;