import React from 'react';
import { render, screen } from '@testing-library/react';
import InputForm from './InputForm';

test('renders learn react link', () => {
  render(<InputForm />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
