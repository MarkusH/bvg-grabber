gl.setup(1680, 945)
json = require("json")
font = resource.load_font("light.ttf")
font2 = resource.load_font("light.ttf")
background = resource.load_image("whitepixel.png")

maxCharWidth = WIDTH/0.6
color = { r = 0.95, g = 0.95, b = 0.0 }
charSize = 82

function alignRight(num)
	--              0   1   2   3   4   5   6   7   8   9  
	local width = { 5, 30,  7,  5,  7, 15,  8,  5,  5,  5 }
	local num1 = num % 10;
    local num2 = math.floor(num / 10 % 10);
	
	if num2 >= 1 then
		return width[num1 + 1] + width[num2 + 1]
	else
		return width[num1 + 1] + 44
	end
end

function node.render()
    local i = 0
    local station_json = json.decode(text)
	background:draw(0, 0, WIDTH, HEIGHT/10)
	background:draw(0, HEIGHT - HEIGHT/10, WIDTH, HEIGHT)
    for k, stations in pairs(station_json) do
        local station = stations[1]
        width = math.floor(maxCharWidth/72/2 + string.len(station)/2)
		font2:write(15, HEIGHT - charSize, station:gsub(" %(Berlin%)", ""), 72, 0,0,0, 1)
		font2:write(15, 30, "Line       Destination                                          Departure", 64, 0,0,0,1)
        i = i + 124
	j = 0
        for k, departures in pairs(stations[2]) do
            local remaining = math.floor(departures['remaining']/60)
            if remaining >= 5 and j < 8 then
		j = j + 1
                local timeString = string.format('%2d min', remaining)
                font:write(WIDTH-440 + alignRight(remaining), i,
                           string.format('%14s', timeString),
                           charSize, color.r, color.g, color.b, 1) 
            	font:write(0, i,
                	       string.format(' %-5s',
                    	                 departures['line']:gsub("Bus ", "")),
                       	   charSize, color.r, color.g, color.b, 1)
				font:write(250, i,
                           string.format(' %-32s',
                                         departures['end']:gsub("-", '—'):gsub('%(Berlin%)', '')),
                           charSize, color.r, color.g, color.b, 1)
            	i = i + charSize + 10
			end
        end
    end
end

util.file_watch("ERP", function(content)
	text = content
end)

