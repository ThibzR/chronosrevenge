import React from "react";
import styled from "styled-components";

type Props = {
    title: string,
    subtitle: string,
}

const Container = styled.div`
  display: flex;
  position: fixed;
  top:0;
  width: 100%;
  z-index:100;
  flex-direction: row;
  justify-content: space-between;
  align-items: baseline;
`;

const Header: React.FC<Props> = ({title, subtitle}) => (
    <Container>
        <text>{title}</text>
        <text>{subtitle}</text>
    </Container>
);

export default Header;