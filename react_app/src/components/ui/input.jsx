import React from 'react';

export const Input = ({ value, onChange, placeholder }) => {
  return <input value={value} onChange={onChange} placeholder={placeholder} />;
};
