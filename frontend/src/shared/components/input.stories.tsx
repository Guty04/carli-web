import type { Meta, StoryObj } from "@storybook/nextjs-vite";
import { Search } from "lucide-react";
import { Input } from "./input";

const meta = {
  title: "shared/Input",
  component: Input,
  argTypes: {
    label: { control: "text" },
    error: { control: "text" },
    helperText: { control: "text" },
    placeholder: { control: "text" },
    disabled: { control: "boolean" },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { label: "Project Name", placeholder: "my-project" },
};

export const WithHelperText: Story = {
  args: {
    label: "Description",
    placeholder: "Enter description...",
    helperText: "Max 500 characters",
  },
};

export const WithError: Story = {
  args: {
    label: "Email",
    placeholder: "your@email.com",
    error: "Invalid email address",
    defaultValue: "invalid-email",
  },
};

export const WithLeftIcon: Story = {
  args: {
    label: "Search",
    placeholder: "Search projects...",
    leftIcon: <Search size={16} />,
  },
};

export const Disabled: Story = {
  args: {
    label: "Read Only",
    placeholder: "Cannot edit",
    disabled: true,
    defaultValue: "Locked value",
  },
};

export const AllStates: Story = {
  render: () => (
    <div className="flex w-[400px] flex-col gap-(--space-6)">
      <Input label="Default" placeholder="Type here..." />
      <Input
        label="With Helper"
        placeholder="Type here..."
        helperText="Some guidance text"
      />
      <Input
        label="With Error"
        placeholder="Type here..."
        error="This field is required"
      />
      <Input
        label="With Icon"
        placeholder="Search..."
        leftIcon={<Search size={16} />}
      />
      <Input label="Disabled" placeholder="Disabled" disabled />
    </div>
  ),
};
