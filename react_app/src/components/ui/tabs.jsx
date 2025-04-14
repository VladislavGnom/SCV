import React, { useState } from 'react';

export const Tabs = ({ tabs }) => {
  const [active, setActive] = useState(0);
  return (
    <div>
      <div style={{ display: 'flex', gap: '10px' }}>
        {tabs.map((tab, idx) => (
          <button key={idx} onClick={() => setActive(idx)}>
            {tab.label}
          </button>
        ))}
      </div>
      <div style={{ marginTop: '10px' }}>{tabs[active].content}</div>
    </div>
  );
};