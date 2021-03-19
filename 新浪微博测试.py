params = (
    ('uid', '2882591901'),
    ('page', '1'),
    ('feature', '0'),
)
lisy = [1,2,3,4,5,6,7,8]
for i in lisy:
    params = dict(params)
    params["uid"] = i
    print(params)
print(params)