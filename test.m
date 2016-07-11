raw = csvread('sh50.txt');
raw = raw(:,3:end); % only keep open, high, low, close
raw = raw(:,1:end-1); % remove vol

%calculate percentage 
per_raw = raw(1,:)./raw(1,1); % day 1
per_raw = [per_raw; raw(2:end,:)./raw(1:end-1,4)]; %day t based on day t01
per_raw = (per_raw -1)*10; % times 10 to be close to 1. next step should be normalize it



%create x days consecutive matrix
K =20;
d5_price = zeros(size(per_raw,1)-K+1,K*4); 
for i = 1:K
  d5_price(:,(i-1)*4+1:(i-1)*4+4) = per_raw(i:end-K+i,:);
end;

d5_cum = d5_price; % calculate cumulative change

for i = 1:(K-1)
  d5_cum(:,i*4+1:i*4+4)=d5_cum(:,i*4+1:i*4+4)+d5_cum(:,(i-1)*4+4);
end

d5_category(find(d5_cum(:,end)>0.3)) = 1; % categorize to -3%-, -3~3, 3%+
d5_category(find(d5_cum(:,end)<=0.3)) = 2;
d5_category(find(d5_cum(:,end)<=-0.3)) = 3;
d5_category = d5_category';


hist(max(d5_cum,[],2),30);%max high histogram
% for those up 3% more at the end of 5 days how much down in 5 days
plot(min(d5_cum(find(d5_category==1),:) ,[],2),d5_cum(find(d5_category==1),end),"+")
plot(max(d5_cum(find(d5_category==3),:) ,[],2),d5_cum(find(d5_category==3),end),"+")