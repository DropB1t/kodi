export default function displayClock() {
  const monthNames = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ];

  var d = new Date();
  var mm = monthNames[d.getMonth()];
  var dd = d.getDate();
  var min = ('0' + d.getMinutes()).slice(-2);
  var hh = d.getHours();

  var data = hh + ":" + min + " | " + mm + "  " + dd
  $('#time-date-widget span').text(data)

}
