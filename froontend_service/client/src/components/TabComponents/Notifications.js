import React, { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { useAuth } from "../../context/Auth/AuthProvider";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { classNames } from "primereact/utils";
import "../../assets/css/FormDemo.css";
import { useSocket } from "../../context/Socket/SocketProvider";
import { Card } from "primereact/card";

const URL = "http://notification-service-jfs4.k3s";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [pushNotifications, setPushNotifications] = useState([]);
  const auth = useAuth();
  const socket = useSocket();

  const defaultValues = {
    text: "",
    email: "",
  };

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({ defaultValues });

  useEffect(() => {
    const handleReceiveNotification = (notification) => {
      setNotifications([...notifications, notification]);
    };
    socket.on("newNotification", handleReceiveNotification);
    return () => {
      socket.off("newNotification", handleReceiveNotification);
    };
  }, [socket, notifications]);

  useEffect(() => {
    fetch(URL + "/notifications", {
      headers: {
        Authorization: auth.user.token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let result = JSON.parse(data);
        setPushNotifications(result);
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  }, [auth.user.token]);

  const handleNewNotification = async (values) => {
    const data = {
      text: "oi",
      uid: auth.getId(),
      options: {},
    };

    try {
      const response = await fetch(URL + "/notification", {
        method: "POST",
        headers: {
          Authorization: auth.getId(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    } catch (err) {
      console.error("Error:", err);
    }
  };

  const getFormErrorMessage = (name) => {
    return (
      errors[name] && <small className="p-error">{errors[name].message}</small>
    );
  };

  return (
    <>
      <div className="card">
        <h1>Notifications</h1>
        <form
          onSubmit={handleSubmit(handleNewNotification)}
          className="p-fluid"
        >
          <div className="field pb-1 ">
            <span className="p-float-label p-input-icon-right">
              <i className="pi pi-envelope" />
              <Controller
                name="email"
                control={control}
                rules={{
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
                    message: "Invalid email address. E.g. example@email.com",
                  },
                }}
                render={({ field, fieldState }) => (
                  <InputText
                    id={field.name}
                    {...field}
                    className={classNames({
                      "p-invalid": fieldState.error,
                    })}
                  />
                )}
              />
              <label
                htmlFor="email"
                className={classNames({ "p-error": !!errors.email })}
              >
                Email*
              </label>
            </span>
            {getFormErrorMessage("email")}
          </div>
          <div className="field pb-1">
            <span className="p-float-label">
              <Controller
                name="text"
                control={control}
                rules={{ required: "Text is required." }}
                render={({ field, fieldState }) => (
                  <InputText
                    id={field.name}
                    {...field}
                    className={classNames({
                      "p-invalid": fieldState.error,
                    })}
                  />
                )}
              />
              <label
                htmlFor="text"
                className={classNames({ "p-error": errors.password })}
              >
                Text*
              </label>
            </span>
          </div>

          <Button type="submit" label="Submit" className="mt-2" />
        </form>
      </div>
      <h1> Notifications sended </h1>
      {pushNotifications.map((notification, index) => (
        <div key={index}>
          <span>Value: {notification.txt}</span>
        </div>
      ))}
      <h1> Notifications Received </h1>
      {notifications.map((notification, index) => (
        <Card title={"Notification: " + index} key={index} className="mt-2 mx-2">
          <div className="flex flex-column align-items-start">
            <span>User: {notification.uid}</span>
            <span>Value: {notification.txt}</span>
          </div>
        </Card>
      ))}
    </>
  );
}
