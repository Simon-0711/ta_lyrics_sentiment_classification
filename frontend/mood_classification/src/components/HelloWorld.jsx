import React, { useEffect, useState } from "react";
import backendUrl from "../config";

const MessageContext = React.createContext({
  message: [], fetchMessage: () => {}
})

export default function Message() {
    const [message, setMessage] = useState([])
    const fetchMessage = async () => {
        const response = await fetch(backendUrl+"/dummy-endpoint")
        const backendMessage = await response.json()
        setMessage(backendMessage.message)
    }
    useEffect(() => {
        fetchMessage()
      }, [])

    return(
    <MessageContext.Provider value={{message, fetchMessage}}>
          <b>{message}</b>
    </MessageContext.Provider>
    )
}
