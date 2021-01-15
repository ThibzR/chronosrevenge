import React from 'react';
import Header from "./molecules/Header";
import Content from "./components/Content";

const App: React.FC = () => {
  return (
    <div className="App">
      <Header title="CHRONOS Revenge" subtitle="ThibzR ManneGd" />
      <Content />
    </div>
  );
}

export default App;
