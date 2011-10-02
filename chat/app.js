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

var chat = io.of('/chat');

chat.on('connection', function(socket) {
  socket.emit('message', { hey: 'you' })
  
  socket.on('disconnect', function() {})
})

// Routes
app.post('/message', function(req, res){
  var conversation_id = req.body.conversation_id;
  var user_type = req.body.user_type;
  var message = req.body.message;
  
  io.sockets.in(conversation_id).emit('message', { user_type: user_type, message: message })
  
  res.write('{success:true}');
});

app.listen(3000);
console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);