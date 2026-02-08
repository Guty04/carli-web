import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Select } from "./select";

const sampleOptions = [
  { value: "backend", label: "Backend" },
  { value: "frontend", label: "Frontend" },
  { value: "fullstack", label: "Fullstack" },
];

const meta = {
  title: "shared/Select",
  component: Select,
  args: {
    options: sampleOptions,
  },
  argTypes: {
    label: { control: "text" },
    error: { control: "text" },
    helperText: { control: "text" },
    placeholder: { control: "text" },
    disabled: { control: "boolean" },
  },
} satisfies Meta<typeof Select>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { label: "Project Type", placeholder: "Select type..." },
};

export const WithHelperText: Story = {
  args: {
    label: "Project Type",
    placeholder: "Select type...",
    helperText: "Choose the project category",
  },
};

export const WithError: Story = {
  args: {
    label: "Project Type",
    placeholder: "Select type...",
    error: "Project type is required",
  },
};

export const Disabled: Story = {
  args: {
    label: "Project Type",
    disabled: true,
    defaultValue: "backend",
  },
};
