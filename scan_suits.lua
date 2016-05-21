dofile("FindItems.lua")

UO.CliNr = 1
Ignore = {}

function scan()
  local writeStr = ""
  local playerId = 0
  players = ScanItems(false, {Type={400,401,605,606,667,666,217,225}}, Ignore)
  local nYear,nMonth,nDay,nDayOfWeek = getdate()
  local nHour, nMinute, nSecond, nMillisec = gettime()
  local date = nYear .. nMonth .. nDay
  local time = nHour .. nMinute .. nSecond
  for i=1, #players do
    playerId = players[i].ID
    playerType = players[i].Type
    local playerName, playerInfo = UO.Property(playerId)
    
    if string.len(playerName) > 0 then
      print("processing " .. playerName)
    
      writeStr = writeStr .. "****" .. "\n" .. date .. "$" .. time .. "$" .. playerId .. "$" .. playerType .. "$" .. playerName .. "$" .. playerInfo .. "\n" 
    
      items = ScanItems(false, {ContID=playerId})
      for i=1, #items do
        itemId = items[i].ID
        itemType = items[i].Type
        local itemName, itemInfo = UO.Property(itemId)
        itemInfo = string.gsub(itemInfo, "\n", "$")
        if itemName then
          writeStr = writeStr .. itemId .. "$" .. itemType .. "$" .. itemName .. "$" .. itemInfo .. "\n"
        end
      end 
      IgnoreItem(Ignore, playerId)
    end
  end
  
  local f, e = openfile("suit.txt", "a")
  if f then
    f:write(writeStr)
    f:close()
  else
    error(e, 2)
  end
end

while true do
  scan()
end



--i = 0
--while i ~= nCnt do
--  local id,type,kind,contId,x,y,stack,rep,col = UO.GetItem(i)
--  local name, info = UO.Property(id)
--  print(id .. ':' .. name .. ':' .. info .. ':' .. type .. ':' .. contId .. ':' .. col)
--  i = i + 1
--end

--wait(1000)
--UO.Msg("Hi, my name is " .. UO.CharName .. "!\n")
--print("UO.Clocal id,type,kind,contId,x,y,stack,rep,col = UO.GetItem(iharName = " .. UO.CharName)