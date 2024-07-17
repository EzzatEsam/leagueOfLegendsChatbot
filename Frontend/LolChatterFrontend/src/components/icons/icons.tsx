// icon:calendar_day | System UIcons https://systemuicons.com/ | Corey Ginnivan
import * as React from "react";

function IconCalendar_day(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 21 21"
      fill="currentColor"
      height="1em"
      width="1em"
      {...props}
    >
      <g fill="none" fillRule="evenodd" transform="translate(2 2)">
        <path
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M2.5.5h12.027a2 2 0 012 2v11.99a2 2 0 01-1.85 1.995l-.16.006-12.027-.058a2 2 0 01-1.99-2V2.5a2 2 0 012-2zM.5 4.5h16.027"
        />
        <path
          fill="currentColor"
          d="M5.5 8.5 A1 1 0 0 1 4.5 9.5 A1 1 0 0 1 3.5 8.5 A1 1 0 0 1 5.5 8.5 z"
        />
      </g>
    </svg>
  );
}

function IconWrite(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      viewBox="0 0 21 21"
      fill="currentColor"
      height="1em"
      width="1em"
      {...props}
    >
      <g
        fill="none"
        fillRule="evenodd"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M17 4a2.121 2.121 0 010 3l-9.5 9.5-4 1 1-3.944 9.504-9.552a2.116 2.116 0 012.864-.125zM9.5 17.5h8M15.5 6.5l1 1" />
      </g>
    </svg>
  );
}
export { IconCalendar_day, IconWrite };
