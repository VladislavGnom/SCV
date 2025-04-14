import React from 'react';
// import './card.css'; // можно добавить стили

export const Card = ({ children }) => {
  return <div className="card">{children}</div>;
};
