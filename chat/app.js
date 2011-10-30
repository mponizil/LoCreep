var express = require('express');

var app = module.exports = express.createServer();

// Configuration
app.configure(function(){
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});

app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true })); 
});

app.configure('production', function(){
  app.use(express.errorHandler()); 
});

// socket.io begins
var io = require('socket.io').listen(app);
io.set('log level',2);

io.sockets.on('connection', function(socket) {
  
  socket.on('group.init', function(data) {
    socket.join('group' + data.group_id);
  });
  socket.on('conversation.init', function(data) {
    socket.join('conv' + data.conversation_id);
  });
  
  socket.on('disconnect', function() {});
});

// Routes
app.post('/message', function(req, res) {
  var params = {
    group_id: req.body.group_id,
    conversation_id: req.body.conversation_id,
    user_type: req.body.user_type,
    body: req.body.message
  };
  
  if (params.user_type == 'creep') params.creep_phone = req.body.creep_phone;
  io.sockets.in('group' + params.group_id).emit('message', params);
  io.sockets.in('conv' + params.conversation_id).emit('message', params);
  
  res.write('{success:true}');
  res.end();
});

app.listen(3000);
console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);