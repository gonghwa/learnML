clear;
raw = csvread('sh50.txt');
raw = raw(:,3:end); % only keep open, high, low, close
raw = raw(:,1:end-1); % remove vol

%calculate percentage of T day's price based on T-1 close
per_raw = raw(1,:)./raw(1,1); % day 1 based on open of day 1
per_raw = [per_raw; raw(2:end,:)./raw(1:end-1,4)]; %day t based on day t-1 close
per_raw = (per_raw -1); % times 10 to be close to 1. next step should be normalize it


%create K days consecutive matrix with M cumulated price index
K =22; M=5;
daily_price = zeros(size(per_raw,1)-K+1,K*4); 
for i = 1:K
  daily_price(:,(i-1)*4+1:(i-1)*4+4) = per_raw(i:end-K+i,:);
end;

% split into K-M days price index and Last M days cumulative change
daily_cum = daily_price(:,end-M*4+1:end); 
daily_price = daily_price(:,1:end-M*4);

% normalize daily_price data
mu = mean (daily_price);
sigma = std(daily_price);
X_norm = (daily_price-mu)./sigma;

for i = 1:(M-1)
  daily_cum(:,i*4+1:i*4+4)=daily_cum(:,i*4+1:i*4+4)+daily_cum(:,(i-1)*4+4);
end

% build 3 categories by devide 
onethird = floor(size(daily_cum,1)/3);
cate1 = sort(daily_cum(:,end))(onethird*2+1,:);
cate2 = sort(daily_cum(:,end))(onethird+1,:);
Y_category(find(daily_cum(:,end)>cate1)) = 1; % categorize to -3%-, -3~3, 3%+
Y_category(find(daily_cum(:,end)<=cate1)) = 2;
Y_category(find(daily_cum(:,end)<=cate2)) = 3;
Y_category = Y_category';


% for those up 3% more at the end of 5 days how much down in 5 days
%hist(max(daily_cum,[],2),30);%max high histogram
%plot(min(daily_cum(find(Y_category==1),:) ,[],2),daily_cum(find(Y_category==1),end),"+")
%plot(max(daily_cum(find(Y_category==3),:) ,[],2),daily_cum(find(Y_category==3),end),"+")
%plot(sort(daily_cum(:,end))(onethird*2:end,:))

days_of_sample = size(daily_price,1);
rand_seq = randperm(days_of_sample)';
X=X_norm(1:rand_seq(round(days_of_sample*0.7),:)
X_test=X_norm(rand_seq(round(days_of_sample*0.7)+1:end,:)

%model = svmtrain(Y_category , X_norm , '-c 10 -g 0.1');
