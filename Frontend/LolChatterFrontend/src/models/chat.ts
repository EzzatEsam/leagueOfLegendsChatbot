export interface chat {
    id: number,
    title : string,
    date : Date,
}

export  interface chatMessage {
    id: number ,
    chatId : number | string,
    content : string,
    role : string,
    date : Date,
}

