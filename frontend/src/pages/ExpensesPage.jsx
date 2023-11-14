import React, { useEffect, useState } from "react";

import { googleLogout, useGoogleLogin } from "@react-oauth/google";
import {
  creatExpenses,
  deleteExpenses,
  getAllExpenses,
  getFilterExpenses,
  login,
  updateExpenses,
  updateUser,
} from "../api/expensesService";

import {
  clearAccessToken,
  setAccessToken,
} from "../helpers/accessToken.helper";
import {
  clearActiveUser,
  getActiveUser,
  setActiveUser,
  updateActiveUser,
} from "../helpers/user.helper";

const ExpensesPage = () => {
  const [expenses, setExpenses] = useState(null);
  const [isShowCabinet, setIsShowCabinet] = useState(false);
  const [isShowSearch, setIsShowSearch] = useState(false);
  const [isShowAdd, setIsShowAdd] = useState(false);
  const [dateFrom, setDateFrom] = useState(undefined);
  const [dateTo, setDateTo] = useState(undefined);
  const [date, setDate] = useState(undefined);
  const [timeFrom, setTimeFrom] = useState(undefined);
  const [timeTo, setTimeTo] = useState(undefined);
  const [time, setTime] = useState(undefined);
  const [item, setItem] = useState("");
  const [firstName, setFirstName] = useState(undefined);
  const [lastName, setLastName] = useState(undefined);
  const [cost, setCost] = useState(undefined);
  const [user, setUser] = useState(null);
  const [expensesId, setExpensesId] = useState(null);
  const [costIndicator, setCostIndicator] = useState(null); // -1 | 0 | 1 | null
  let activeUser = getActiveUser();
  const [dayLimit, setDayLimit] = useState(undefined);

  const fetchExpenses = async () => {
    const expenses = await getAllExpenses();
    setExpenses(expenses);
    setCostIndicator(null);
  };

  useEffect(() => {
    if (activeUser) {
      fetchExpenses()
    }
  }, []);

  function refreshPage() {
    window.location.reload(false);
  }

  const handleLogin = useGoogleLogin({
    onSuccess: async (res) => {
      const userData = await login(res.access_token);
      setAccessToken(userData.access_token);
      setActiveUser(userData);
      await fetchExpenses();
      setUser(userData);
    },
    onError: (error) => {
      console.error(error);
    },
  });

  const handleLogout = async () => {
    // await logout();
    googleLogout();
    clearAccessToken();
    clearActiveUser();
    setUser(null);
    refreshPage();
  };

  const showCabinet = () => {
    setIsShowSearch(false);
    setIsShowAdd(false);
    setIsShowCabinet(true);
  };

  const showSearch = () => {
    // setIsShowLimit(false);
    setIsShowCabinet(false);
    setIsShowAdd(false);
    setIsShowSearch(true);
  };

  const showAdd = () => {
    setIsShowCabinet(false);
    setIsShowSearch(false);
    // setIsShowLimit(false);
    setIsShowAdd("add");
  };

  const editUser = (user) => {
    setFirstName(user.firstName);
    setLastName(user.lastName);
    setDayLimit(user.dayLimit);
    setIsShowCabinet(true);
  };

  const updUser = (event) => {
    event.preventDefault();
    setIsShowCabinet(false);
    updateUser(activeUser.id, {
      user: activeUser.id,
      first_name: firstName,
      last_name: lastName,
      day_sum: dayLimit,
    })
      .then((userData) => {
        console.log(userData);
        updateActiveUser(userData);
        activeUser = getActiveUser();
        setFirstName(activeUser.first_name);
        setLastName(activeUser.last_name);
        setDayLimit(activeUser.day_sum);
        fetchExpenses();
      })
      .catch((error) => {
        console.error("Update user error", error);
      });
  };

  const searchExpenses = (event) => {
    event.preventDefault();
    setIsShowSearch(false);
    getFilterExpenses({
      user,
      date_from: dateFrom,
      date_to: dateTo,
      time_from: timeFrom,
      time_to: timeTo,
      item,
    })
      .then((data) => {
        setExpenses(data);
        setDateFrom(undefined);
        setDateTo(undefined);
        setTimeFrom(undefined);
        setTimeTo(undefined);
        setItem("");
        setCostIndicator(null);
      })
      .catch((error) => {
        console.error("Search expenses error", error);
      });
  };

  const addExpenses = (event) => {
    event.preventDefault();
    setIsShowAdd(false);
    creatExpenses({ user: activeUser.id, date, time, item, cost })
      .then(() => {
        fetchExpenses();
        setDate(undefined);
        setTime(undefined);
        setItem(undefined);
        setCost(undefined);
      })
      .catch((error) => {
        console.error("Add expenses error", error);
      });
  };

  const editExpenses = (expenses) => {
    setDate(expenses.date);
    setTime(expenses.time);
    setItem(expenses.item);
    setCost(expenses.cost);
    setExpensesId(expenses.id);
    setIsShowAdd("edit");
  };

  const updExpenses = (event) => {
    event.preventDefault();
    setIsShowAdd(false);
    updateExpenses(expensesId, { user: activeUser.id, date, time, item, cost })
      .then(() => {
        fetchExpenses();
        setDate(undefined);
        setTime(undefined);
        setItem(undefined);
        setCost(undefined);
      })
      .catch((error) => {
        console.error("Update expenses error", error);
      });
  };

  const delExpenses = (expense) => {
    deleteExpenses(expense.id)
      .then(() => {
        fetchExpenses();
      })
      .catch((error) => {
        console.error("Delete expenses error", error);
      });
  };

  useEffect(() => {
    console.log("expenses: ", expenses);
  }, [expenses]);
  const TableLines = ({ items }) =>
    items.map((item) => (
      <tr
        key={item.id}
        className={`${item.over_day_limit ? "text-success" : "text-danger"}`}
      >
        <td>{item.id}</td>
        <td>{item.date}</td>
        <td>{item.time}</td>
        <td>{item.item}</td>
        <td>{item.cost}</td>
        <td>
          <button
            className="btn btn-primary me-3"
            onClick={() => editExpenses(item)}
          >
            Edit
          </button>
          <button className="btn btn-danger" onClick={() => delExpenses(item)}>
            Delete
          </button>
        </td>
      </tr>
    ));

  return (
    <div>
      <nav className="navbar bg-body-tertiary">
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1"></span>
          {activeUser ? (
            <div className="d-flex gap-3">
              <img
                className="rounded-circle"
                src={activeUser.avatar}
                alt="Avatar"
                width={50}
                height={50}
              />
              <button
                className="btn btn-outline-primary me-2"
                type="button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          ) : (
            <button
              className="btn btn-outline-primary me-2"
              type="button"
              onClick={handleLogin}
            >
              Login
            </button>
          )}
        </div>
      </nav>

      {activeUser && (
        <div className="p-4">
          <div className="d-flex justify-content-center mb-4">
            <button
              type="button"
              className="btn btn-primary me-3"
              onClick={showCabinet}
            >
              Cabinet
            </button>
            <button
              type="button"
              className="btn btn-primary me-3"
              onClick={showSearch}
            >
              Search
            </button>
            <button type="button" className="btn btn-primary" onClick={showAdd}>
              Add
            </button>
          </div>

          {isShowCabinet && (
            <div className="mb-5">
              <form className="row g-3" onSubmit={updUser}>
                <div className="col-12">
                  <label htmlFor="firstName" className="form-label">
                    First name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    name="first_name"
                    placeholder={activeUser.first_name}
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="lastName" className="form-label">
                    Last name
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    name="last_name"
                    placeholder={activeUser.last_name}
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="dayLimit" className="form-label">
                    Day limit
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-control"
                    name="day_sum"
                    placeholder={activeUser.day_sum}
                    value={dayLimit}
                    onChange={(e) => setDayLimit(e.target.value)}
                  />
                </div>
                <div>
                  <button
                    type="reset"
                    className="btn btn-primary me-3"
                    onClick={() => {
                      setIsShowCabinet(false);
                      setFirstName(firstName);
                      setLastName(lastName);
                      setDayLimit(dayLimit);
                    }}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Update
                  </button>
                </div>
              </form>
            </div>
          )}

          {isShowSearch && (
            <div className="mb-5">
              <form className="row g-3" onSubmit={searchExpenses}>
                <div className="col-12">
                  <label htmlFor="dateFrom" className="form-label">
                    Date from
                  </label>
                  <input
                    type="date"
                    className="form-control"
                    name="dateFrom"
                    placeholder="Date from"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="dateTo" className="form-label">
                    Date to
                  </label>
                  <input
                    type="date"
                    className="form-control"
                    name="dateTo"
                    placeholder="Date to"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="timeFrom" className="form-label">
                    Time from
                  </label>
                  <input
                    type="time"
                    className="form-control"
                    name="timeFrom"
                    placeholder="Time from"
                    value={timeFrom}
                    onChange={(e) => setTimeFrom(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="timeTo" className="form-label">
                    Time to
                  </label>
                  <input
                    type="time"
                    className="form-control"
                    name="timeTo"
                    placeholder="Time to"
                    value={timeTo}
                    onChange={(e) => setTimeTo(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="item" className="form-label">
                    Item
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    name="item"
                    placeholder="Item"
                    value={item}
                    onChange={(e) => setItem(e.target.value)}
                  />
                </div>
                <div>
                  <button
                    type="reset"
                    className="btn btn-primary me-3"
                    onClick={() => {
                      setIsShowSearch(false);
                      setDateFrom(undefined);
                      setDateTo(undefined);
                      setTimeFrom(undefined);
                      setTimeTo(undefined);
                      setItem(undefined);
                    }}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Search
                  </button>
                </div>
              </form>
            </div>
          )}

          {isShowAdd && (
            <div className="mb-5">
              <form
                className="row g-3"
                onSubmit={isShowAdd === "add" ? addExpenses : updExpenses}
              >
                <div className="col-12">
                  <label htmlFor="date" className="form-label">
                    Date
                  </label>
                  <input
                    type="date"
                    className="form-control"
                    name="date"
                    placeholder="Date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="time" className="form-label">
                    Time
                  </label>
                  <input
                    type="time"
                    className="form-control"
                    name="time"
                    placeholder="Time"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="item" className="form-label">
                    Item
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    name="item"
                    placeholder="Item"
                    value={item}
                    onChange={(e) => setItem(e.target.value)}
                  />
                </div>
                <div className="col-12">
                  <label htmlFor="cost" className="form-label">
                    Cost
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-control"
                    name="cost"
                    placeholder="Cost"
                    value={cost}
                    onChange={(e) => setCost(e.target.value)}
                  />
                </div>
                <div>
                  <button
                    type="reset"
                    className="btn btn-primary me-3"
                    onClick={() => {
                      setIsShowAdd(false);
                      setDate(undefined);
                      setTime(undefined);
                      setItem(undefined);
                      setCost(undefined);
                    }}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {isShowAdd === "add" ? "Add" : "Save"}
                  </button>
                </div>
              </form>
            </div>
          )}

          <table className="table">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Date</th>
                <th scope="col">Time</th>
                <th scope="col">Item</th>
                <th scope="col">Cost</th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              {!!expenses &&
                Object.entries(expenses).map(([baseDate, items]) => (
                  <>
                    <tr>
                      <td colSpan="6" className="text-center">
                        {baseDate}
                      </td>
                    </tr>
                    <TableLines items={items} />
                  </>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ExpensesPage;
