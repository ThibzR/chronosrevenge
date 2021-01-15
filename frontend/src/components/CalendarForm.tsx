import React, {useState} from "react";
import styled from "styled-components";
import { Formik, Form, Field } from 'formik';

type Values = {
    group: string;
    blacklistCourses?: string[];
    login?: string;
    password?: string;
}

const Container = styled.div`
  flex: 50%;
`;

const CalendarForm: React.FC = () => {
    const initialValues: Values = { group: '' };

    const [blacklist, setBlacklist] = useState<boolean>(false);
    return (
        <Container>
            <Formik
                initialValues={initialValues}
                onSubmit={() => alert('Form submitted')}
            >
                <Form>
                    <label htmlFor="group">Your group</label>
                    <Field name="group" type="text" />
                    <label htmlFor="blacklist">Do you want to blacklist some courses?</label>
                    <button type='button' onClick={() => setBlacklist(!blacklist)}>Blacklist</button>
                    <label htmlFor="login">Login</label>
                    <Field name="login" type="text" />
                    <label htmlFor="password">Password</label>
                    <Field name="password" type="text" />
                    <button type="submit">Submit</button>
                </Form>
            </Formik>
        </Container>
    );
}

export default CalendarForm;