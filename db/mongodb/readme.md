<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN""http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
      <key>Label</key>
      <string>mongodb</string>
      
      <key>ProgramArguments</key>
      <array>
        <string>/usr/local/mongodb/bin/mongod</string>
      </array>
      
      <key>RunAtLoad</key>
      <true/>
      
      <key>KeepAlive</key>
      <true/>
      
      <key>WorkingDirectory</key>
      <string>/usr/local/mongodb</string>
      
      <key>StandardErrorPath</key>
      <string>/var/log/mongodb/error.log</string>
      
      <key>StandardOutPath</key>
      <string>/var/log/mongodb/output.log</string>
  </dict>
</plist>
