document.addEventListener('DOMContentLoaded', function() {
    const calendar = document.getElementById('calendar');
    const form = document.getElementById('appointment-details');
    let currentView = 'week';
    let currentDate = new Date();
    let appointments = [];

    function renderCalendar() {
        let html = '<table><thead><tr>';
        if (currentView === 'month') {
            html += '<th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th>';
        } else {
            html += '<th>Time</th>';
            for (let i = 0; i < (currentView === 'week' ? 7 : 1); i++) {
                html += `<th>${getFormattedDate(addDays(currentDate, i))}</th>`;
            }
        }
        html += '</tr></thead><tbody>';
        
        if (currentView === 'month') {
            html += renderMonthView();
        } else if (currentView === 'week') {
            html += renderWeekView();
        } else {
            html += renderDayView();
        }
        
        html += '</tbody></table>';
        calendar.innerHTML = html;
    }

    function renderMonthView() {
        let html = '';
        const monthStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        const monthEnd = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
        const startDate = new Date(monthStart);
        startDate.setDate(startDate.getDate() - startDate.getDay());
        const endDate = new Date(monthEnd);
        endDate.setDate(endDate.getDate() + (6 - endDate.getDay()));

        while (startDate <= endDate) {
            html += '<tr>';
            for (let i = 0; i < 7; i++) {
                const day = new Date(startDate);
                html += `<td>${day.getDate()}${renderAppointmentsForDay(day)}</td>`;
                startDate.setDate(startDate.getDate() + 1);
            }
            html += '</tr>';
        }
        return html;
    }

    function renderWeekView() {
        let html = '';
        for (let hour = 9; hour < 18; hour++) {
            html += '<tr>';
            html += `<td>${hour}:00</td>`;
            for (let day = 0; day < 7; day++) {
                const currentDay = addDays(currentDate, day);
                html += `<td>${renderAppointmentsForHour(currentDay, hour)}</td>`;
            }
            html += '</tr>';
        }
        return html;
    }

    function renderDayView() {
        let html = '';
        for (let hour = 9; hour < 18; hour++) {
            html += '<tr>';
            html += `<td>${hour}:00</td>`;
            html += `<td>${renderAppointmentsForHour(currentDate, hour)}</td>`;
            html += '</tr>';
        }
        return html;
    }

    function renderAppointmentsForDay(day) {
        return appointments
            .filter(appt => isSameDay(new Date(appt.date), day))
            .map(appt => `<div class="appointment${appt.is_emergency ? ' emergency' : ''}">${appt.patient_name}</div>`)
            .join('');
    }

    function renderAppointmentsForHour(day, hour) {
        return appointments
            .filter(appt => isSameDay(new Date(appt.date), day) && new Date(appt.date + 'T' + appt.time).getHours() === hour)
            .map(appt => `<div class="appointment${appt.is_emergency ? ' emergency' : ''}">${appt.patient_name}</div>`)
            .join('');
    }

    function getFormattedDate(date) {
        return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
    }

    function addDays(date, days) {
        let result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    function isSameDay(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getDate() === date2.getDate();
    }

    function fetchAppointments() {
        fetch('/api/appointments')
            .then(response => response.json())
            .then(data => {
                appointments = data;
                renderCalendar();
            });
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        const appointmentData = Object.fromEntries(formData.entries());
        appointmentData.is_emergency = form.querySelector('#is-emergency').checked;

        fetch('/api/appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(appointmentData),
        })
        .then(response => response.json())
        .then(data => {
            fetchAppointments();
            form.reset();
        });
    });

    document.getElementById('day-view').addEventListener('click', () => {
        currentView = 'day';
        renderCalendar();
    });

    document.getElementById('week-view').addEventListener('click', () => {
        currentView = 'week';
        renderCalendar();
    });

    document.getElementById('month-view').addEventListener('click', () => {
        currentView = 'month';
        renderCalendar();
    });

    // Initial render
    fetchAppointments();
});

