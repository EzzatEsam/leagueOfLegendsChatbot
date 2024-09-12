import React from "react";
import { chat } from "../models/chat";
import { Button, Col, Menu, MenuProps } from "antd";
import * as Icons from "../components/icons/icons";
interface SideBarProps {
  chats: chat[];
  selectedIdx: number | null;
  setSelectedId: (idx: number | null) => void;
}

interface chatGroup {
  day: Date;
  chats: chat[];
}

const isSameDay = (date1: Date, date2: Date) => {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
};

type MenuItem = Required<MenuProps>["items"][number];
const SideBar: React.FC<SideBarProps> = ({
  chats,
  selectedIdx,
  setSelectedId,
}) => {
  const today = new Date();
  const groups: chatGroup[] = [];
  for (let i = 0; i < chats.length; i++) {
    const chatDate = chats[i].date;
    // Check if this date is already in the groups array
    let group = groups.find((g) => isSameDay(g.day, chatDate));

    // If not, create a new group for this date
    if (!group) {
      group = {
        day: new Date(
          chatDate.getFullYear(),
          chatDate.getMonth(),
          chatDate.getDate()
        ),
        chats: [],
      };
      groups.push(group);
    }

    // Add the chat to the group's chats array
    group.chats.push(chats[i]);
  }

  // reverse the order of the groups
  groups.reverse();

  const items: MenuItem[] = groups.map((group, _) => {
    const label = isSameDay(group.day, today)
      ? "Today"
      : `${group.day.getDate()}/${
          group.day.getMonth() + 1
        }/${group.day.getFullYear()}`;
    return {
      icon: <Icons.IconCalendar_day />,
      key: group.day.getTime().toString(),
      type: "group",
      label: label,
      children: group.chats
        .sort((a, b) => b.date.getTime() - a.date.getTime())
        .map((chat, _) => {
          return {
            key: chat.id.toString(),
            label: chat.title,
            onSelect: () => setSelectedId(chat.id),
            onClick: () => setSelectedId(chat.id),
          };
        }),
    };
  });
  return (
    <Col className="p-2 items-center text-center">
      <Button
        className=" my-2"
        onClick={() => {
          setSelectedId(null);
        }}
      >
        Add new
        <Icons.IconWrite />
      </Button>
      <Menu
        className="w-full rounded-md text-left"
        items={items}
        mode="inline"
        style={{ height: "80vh", overflowY: "auto" }}
        selectedKeys={selectedIdx ? [selectedIdx.toString()] : []}
      ></Menu>
    </Col>
  );
};

export default SideBar;
