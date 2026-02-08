import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Textarea } from "./textarea";

const meta = {
  title: "shared/Textarea",
  component: Textarea,
  argTypes: {
    label: { control: "text" },
    error: { control: "text" },
    helperText: { control: "text" },
    placeholder: { control: "text" },
    disabled: { control: "boolean" },
  },
} satisfies Meta<typeof Textarea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { label: "Description", placeholder: "Enter a description..." },
};

export const WithHelperText: Story = {
  args: {
    label: "Description",
    placeholder: "Enter a description...",
    helperText: "Max 500 characters",
  },
};

export const WithError: Story = {
  args: {
    label: "Description",
    placeholder: "Enter a description...",
    error: "Description is too long",
  },
};

export const Disabled: Story = {
  args: {
    label: "Description",
    disabled: true,
    defaultValue: "This cannot be edited",
  },
};
