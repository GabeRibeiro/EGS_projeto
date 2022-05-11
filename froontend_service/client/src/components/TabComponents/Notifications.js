import React, { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { useAuth } from "../../context/AuthProvider";
import createSocket from "../../variables/socket";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { classNames } from "primereact/utils";
import "../../assets/css/FormDemo.css";

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [pushNotifications, setPushNotifications] = useState([]);
  const auth = useAuth();

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
    console.log(auth.user.id);
    createSocket(auth.user.id, handlePushNotification);
  }, []);

  const handlePushNotification = (notification) => {
    console.log(notification);
    setPushNotifications([...pushNotifications, notification]);
  };

  useEffect(() => {
    const url = new URL("http://host.docker.internal:3050/notifications");

    fetch(url, {
      headers: {
        Authorization: auth.user,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setNotifications(data);
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  }, []);

  const handleNewNotification = async (values) => {
    // const headers = {
    //   Authorization: auth.user,
    //   Content,
    // };
    const url = new URL("http://host.docker.internal:3050/notification");

    const data = {
      text: values.text,
      uid: "1",
      options: { email: values.email },
    };

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: auth.user.id,
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
          <div className="field">
            <span className="p-float-label p-input-icon-right">
              <i className="pi pi-envelope" />
              <Controller
                name="email"
                control={control}
                rules={{
                  required: "Email is required.",
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
          <div className="field">
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
      <h1> Notifications sended</h1>
      {pushNotifications.map((notification, index) => (
        <div key={index}>
          <span>User: {notification.uid}</span>
          <span>Value: {notification.txt}</span>
        </div>
      ))}
    </>
  );
}
