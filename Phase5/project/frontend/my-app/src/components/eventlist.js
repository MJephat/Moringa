import React, { useState, useEffect } from 'react';

const EventsList = () => {
  const [events, setEvents] = useState([]);
  useEffect(() => {

    fetch('/events')
      .then(response => response.json())
      .then(data => setEvents(data))
      .catch(error => console.error('Error fetching event:', error));
  }, []);
  const handleDeleteEvent = async (eventId) => {
    try {
      const response = await fetch(`/events/${eventId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete the report.');
      }
      const updatedEvents = events.filter(event => event.id !== eventId);
      setEvents(updatedEvents);
    } catch (error) {
      console.error(error);
    }
  };
  const handleEditField = async (eventId, field, value) => {
    try {
      const response = await fetch(`/events/${eventId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ [field]: value }),
      });
      if (!response.ok) {
        throw new Error(`Failed to update ${field}.`);
      }
      const updatedEvents = Event.map(event => {
        if (event.id === eventId) {
          return { ...event, [field]: value };
        }
        return event;
      });
      setEvents(updatedEvents);
    } catch (error) {
      console.error(error);
    }
  };
  const handleEditMedia = async (eventId, file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await fetch(`http://localhost:5000/events/${eventId}/media`, {
        method: 'PATCH',
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to update media. Server response: ${JSON.stringify(errorData)}`);
      }
      const updatedEvent = await response.json();
      const updatedEvents = events.map(event => {
        if (event.id === eventId) {
          return { ...event, media: updatedEvent.media };
        }
        return event;
      });
      setEvents(updatedEvents);
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <div className="card-grid" style={{ width: '90%',marginLeft: '200px', height: '400px' }}>
      {/* <UserSideBar/> */}
      {events.map(event => (
        <div key={event.id} className="card">
          {/* <button className="delete-btn" onClick={() => handleDeleteEvent(event.id)}>x</button> */}
          <h3>
            <span onClick={() => handleEditField(event.id, 'title', prompt('Enter new title:', event.title))}>
              {event.title}
            </span>
          </h3>
          <p>
            <span onClick={() => handleEditField(event.id, 'host', prompt('Enter new host:', event.host))}>
              Host: {event.host}
            </span>
          </p>
          <p>
            <span onClick={() => handleEditField(event.id, 'location', prompt('Enter new location:', event.location))}>
              Location: {event.location}
            </span>
          </p>
          <p>
            <span onClick={() => handleEditField(event.id, 'time', prompt('Enter new time:', event.time))}>
              Time: {event.time}
            </span>
          </p>
          <p>
            <span onClick={() => handleEditField(event.id, 'date', prompt('Enter new date:', event.date))}>
              Date: {event.date}
            </span>
          </p>
          <div className="card-media">
            <input type="file" accept="image/*" onChange={(e) => handleEditMedia(event.id, e.target.files[0])} />
            <img src={event.media} alt="Event Media" onClick={() => {}} />
          </div>

        </div>
      ))}
    </div>
  );
};
export default EventsList;