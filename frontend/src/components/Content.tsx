import React from "react";
import styled from "styled-components";
import ImagePlaceholder from "./ImagePlaceholder";
import CalendarForm from "./CalendarForm";

const Container = styled.div`
  display: flex;
`;

const Content:React.FC = () => (
    <Container>
        <ImagePlaceholder />
        <CalendarForm />
    </Container>
);

export default Content;